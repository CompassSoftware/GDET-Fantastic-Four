import java.io.*;
import java.lang.ProcessBuilder;
public class main{
    public static void main(String[] args) throws Exception{
        //File file = new File("src/log.txt");
        
        
        
        ProcessBuilder pb = new ProcessBuilder(
            "curl",
            "-i",
            "-u",
            "obrienam:MsTsYnR7826!",
            "https://api.github.com/repos/JaysGitLab/cs5666-javatrix-the-fantastic-four/commits" 
            /**"|",
            "(grep",
            "-E",
            "'name|date|message'",
            "|",
            "grep",
            "-vwE",
            "'payload|\"name\":",
            "\"GitHub\"')"**/
            );
        pb.redirectErrorStream(true);
        Process p = pb.start();
        InputStream is = p.getInputStream();
        BufferedInputStream bi = new BufferedInputStream(is);
        String st;
        BufferedReader br = new BufferedReader(new InputStreamReader(bi));
        
        
        LinkedList cleanup = new LinkedList();
            
        while ((st = br.readLine()) != null){
            cleanup.insert(st.trim());
            //else if(st.substring(1, 8).equals("message")){
            //System.out.println(st);
        }

        
        String[][] info = new String[3][cleanup.getSize() / 3];

        Node curr = cleanup.getHead();

        for(int i = 0; i < cleanup.getSize(); i++){
            info[i % 3][i / 3] = curr.key;
            curr = curr.next;
        }
        
        for(int i = 0; i < info[0].length; i++){
            for(int j = 0; j < info.length; j++){
                System.out.println(info[j][i] + " ");
            }
            System.out.println("");
        }
        //cleanup.print();
        
         
        br.close();
    }
}
