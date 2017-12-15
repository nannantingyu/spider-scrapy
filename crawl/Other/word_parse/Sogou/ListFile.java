import java.io.File;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Map.Entry;
import java.util.LinkedList;
import java.util.ArrayList;

public class ListFile
{
    public static void main(String[] args) throws Exception
    {
        String path = "scel";
        File file = new File(path);
        if(file.exists()) {
            File[] files = file.listFiles();

            if(files.length == 0) {
                System.out.println("文件夹是空的");
            }
            else {
                for(File f: files) {
                    System.out.println(f);
                }
            }
        }
    }
}