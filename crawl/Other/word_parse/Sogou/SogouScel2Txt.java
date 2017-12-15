/**
 * 功能：输入scel的词库文件路径,根据指定路径生成包含该词库文件的词条的txt文件
 */

import java.io.File;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.Paths;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Map.Entry;

/**
 * 解析sogo词库工具类
 */
public class SogouScel2Txt {
    public static void main(String[] args) {
        String path = "scel";
        String outputPath = "../../../data/user_dict.txt";

        File file = new File(path);
        int i = 0;
        if (file.exists()) {
            File[] files = file.listFiles();

            if (files.length == 0) {
                System.out.println("文件夹是空的");
            } else {
                try {
                    RandomAccessFile raf = new RandomAccessFile(outputPath, "rw");
                    for (File f : files) {
                        System.out.println(f.getPath());
                        try {
                            sogou(f.getPath(), raf);
                        } catch (Exception e) {
                            System.out.println(e);
                        }
                    }
                    raf.close();
                } catch (Exception e) {
                    System.out.println(e);
                }
            }
        }
    }

    /**
     * 读取scel的词库文件,生成txt格式的文件
     *
     * @param inputPath  输入路径
     * @param outputPath 输出路径
     * @param isAppend   是否拼接追加词库内容,true 代表追加,false代表重建
     **/

    public static void sogou(String inputPath, RandomAccessFile raf) throws IOException {
        File file = new File(inputPath);
        int count = 0;
        SougouScelMdel model = new SougouScelReader().read(file);
        Map<String, List<String>> words = model.getWordMap(); //词<拼音,词>
        Set<Entry<String, List<String>>> set = words.entrySet();
        Iterator<Entry<String, List<String>>> iter = set.iterator();

        while (iter.hasNext()) {
            Entry<String, List<String>> entry = iter.next();
            List<String> list = entry.getValue();
            int size = list.size();

            for (int i = 0; i < size; i++) {
                String word = list.get(i);
                raf.seek(raf.getFilePointer());
                raf.write((word + "\n").getBytes("utf-8"));
                count++;
            }
        }

        System.out.println("生成成功，总写入" + count + "个词条");
    }

}
