
/**
 * 功能：将百度词库bdict文件中包含的词语转为txt存储，一个词语占一行
 */

import java.io.PrintWriter;
import java.io.File;
import java.util.*;
import java.io.FileWriter;
import java.io.OutputStreamWriter;
import java.io.FileOutputStream;

public class BaiduBdict2Txt {
	/**
	 * 功能: 将输入的bdict文件转为txt文件
	 * @param inputPath: 输入的bdcit文件路径
	 * @param outputPath: 输出的txt文件路径
	 * @return : void
	 */
	public static void transBdict2Txt(String inputPath, String outputPath) throws Exception
	{
		List<String> wordList = new ArrayList<String>();
		wordList = BaiduBdcitReader.readBdictFile(inputPath);
		
		//create outputDirs if not exists
		File outFile = new File(outputPath);
		outFile.getParentFile().mkdirs();

		OutputStreamWriter out = new OutputStreamWriter(new FileOutputStream(outputPath, true), "utf-8");
		for (int i=0;i<wordList.size();i++)
		{
			String word = new String(wordList.get(i).toString().getBytes("UTF-8"), "UTF-8");
//			System.out.println(word);
//			writer.println(word);
			out.write(word+"\n");
		}
		out.close();
		System.out.println(outputPath+ " created \ntotal "+wordList.size()+" words");
		
	}
    
	public static void main(String[] args) throws Exception
	{
		String path = "bcd";
        String outputPath = "../../../data/user_dict.txt";
        File file = new File(path);
        int i = 0;
        if (file.exists()) {
            File[] files = file.listFiles();

            if (files.length == 0) {
                System.out.println("文件夹是空的");
            } else {
                try {
                    for (File f : files) {
                        System.out.println(f.getPath());
                        try {
                            transBdict2Txt(f.getPath(), outputPath);
                        } catch (Exception e) {
                            System.out.println(e);
                        }
                    }
                } catch (Exception e) {
                    System.out.println(e);
                }
            }
        }
	}
}
