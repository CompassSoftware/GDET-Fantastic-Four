import java.io.*;
public class main{
    public static void main(String[] args) throws Exception{
        File file = new File("log.txt");

        BufferedReader br = new BufferedReader(new FileReader(file));

        String st;
        
        LinkedList cleanup = new LinkedList();
            
        while ((st = br.readLine()) != null){
            cleanup.insert(st.trim());
            //else if(st.substring(1, 8).equals("message")){
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

    }
}
