import java.io.*;
public class main{
    
    private static final String dash = "------------------------------------------------------------"
                                     + "------------------------------------------------------------"
                                     + "------------------------------------------------------------"
                                     + "--------------------------------------------------------";
    
    public static void main(String[] args) throws Exception{
        File file = new File("log.txt");

        BufferedReader br = new BufferedReader(new FileReader(file));

        String st;
        
        LinkedList cleanup = new LinkedList();
        
        while ((st = br.readLine()) != null){
            st = st.trim();
            
            if(st.substring(1, 5).equals("name"))
                cleanup.insert(st.substring(9, st.length() - 2));
            
            else if(st.substring(1, 5).equals("date"))
                cleanup.insert(st.substring(9, 19) + ", Time: " + st.substring(20, st.length() - 2));
            
            else if(st.substring(1, 8).equals("message"))
                cleanup.insert(st.substring(11, st.length() - 1));
            
            else
                cleanup.insert(st.trim());
        }

        String[][] info = new String[3][cleanup.getSize() / 3];

        Node curr = cleanup.getHeadNode();

        for(int i = 0; i < cleanup.getSize(); i++){
            info[i % 3][i / 3] = curr.key;
            curr = curr.next;
        }
       
        LinkedList uniqueUsernames = new LinkedList();

        for(int i = 0; i < info[0].length; i++){
            uniqueUsernames.uniqueInsert(info[0][i]);
        }

        curr = uniqueUsernames.getHeadNode();
        
        PrintStream ps = new PrintStream("log.txt");
        
        while(curr != null){
            ps.print(curr.key + " ");
            int count = 0;
            for(int i = 0; i < info[0].length; i++){
                if(curr.key.equals(info[0][i])){
                    count++;
                }
            }
            ps.println(count);
            curr = curr.next;
        }

        ps.format("%-23s%-34s%s\n%s\n", "Username", "Date/Time", "Message", dash); 
        for(int i = 0; i < info[0].length; i++)
            ps.format("%-23s%-34s%s\n%s\n", info[0][i], info[1][i], info[2][i], dash);
    }
}
