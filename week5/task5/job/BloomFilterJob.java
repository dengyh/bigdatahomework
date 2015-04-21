
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URI;
import java.util.Map;
import java.util.StringTokenizer;
import java.util.zip.GZIPInputStream;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.filecache.DistributedCache;
import org.apache.hadoop.fs.FSDataOutputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.hdfs.qjournal.protocol.QJournalProtocolProtos.NewEpochRequestProto;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.util.bloom.BloomFilter;
import org.apache.hadoop.util.bloom.Key;
import org.apache.hadoop.util.hash.Hash;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import com.sun.org.apache.regexp.internal.RE;

public class BloomFilterJob {
	
	public static class BloomFilterMapper extends Mapper<Object, Text, Text, DoubleWritable> {
		private BloomFilter filter = new BloomFilter();
		private String lastLine = "";
		private Boolean firstLine = true;
		
		@Override
		protected void setup(Context context) throws IOException, InterruptedException {
			BufferedReader in = null;
			try {
				Path[] paths = DistributedCache.getLocalCacheFiles(context.getConfiguration());
				for (Path path: paths){
					if (path.toString().contains("bloom.bin")) {
						DataInputStream strm = new DataInputStream(new FileInputStream(path.toString()));
						filter.readFields(strm);
						strm.close();
					}
				}
			} catch (IOException e) {
				e.printStackTrace();
			} finally {
				try {
					if (in != null) {
						in.close();
					}
				} catch (IOException e) { 
					e.printStackTrace();
				}
			}
		}
		
		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
			if (firstLine) {
				firstLine = false;
				return;
			}
			String line = lastLine + value.toString();
			String[] tokens = line.split("\t");
			if (tokens.length < 19) {
				lastLine = line;
				return;
			} else {
				if (filter.membershipTest(new Key(tokens[3].getBytes()))) {
					Text author = new Text();
					author.set(tokens[3]);
					String body = tokens[4];
					DoubleWritable bodyLength = new DoubleWritable();
					bodyLength.set(body.length());
					context.write(author, bodyLength);
				}
				lastLine = "";
			}
		}
	}
	
	public static class BloomFilterReducer extends Reducer<Text, DoubleWritable, Text, DoubleWritable> {
		private DoubleWritable result = new DoubleWritable();
		public void reduce(Text key, Iterable<DoubleWritable> values, Context context) throws IOException, InterruptedException {
			double sum = 0;
			int count = 0;
			for (DoubleWritable val: values) {
				sum += val.get();
				count += 1;
			}
			result.set(sum / count);
			context.write(key, result);
		}
	}
	
	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "Count student post length");
		job.setJarByClass(BloomFilterJob.class);
		job.setMapperClass(BloomFilterMapper.class);
		job.setReducerClass(BloomFilterReducer.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(DoubleWritable.class);
		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		DistributedCache.addCacheFile(new Path("stackoverflow/input/bloom.bin").toUri(), job.getConfiguration());
		int code = job.waitForCompletion(true) ? 0 : 1;
		System.exit(code);
	}
}
