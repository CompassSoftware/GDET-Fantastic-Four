/*
 * This class maintains a set of integers. 
 */
public class LinkedList {
	Node head;
    Node tail;
    int size;

	public LinkedList() {
		head = null;
        tail = null;
        size = 0;
	}
    
    public int getSize(){
        return size;
    }

    public Node getHead(){
        return head;
    }

    /* Insert a key into the set. */
	public void insert(String key) {    
        if (head == null) {
			head = new Node(key, head);
		    size++;
            return;
		}

		Node curr;
		
        for (curr = head; curr.next != null; curr = curr.next){
            if(curr.next.next == null)
                tail = curr;
        }

        if((tail == null || tail.key.equals(key) == false) && (tail == null || tail.next == null || tail.next.key.equals(key) == false)){
            curr.next = new Node(key, curr.next);
            size++;
        }
    }
	
	/* Print the contents of the set in sorted order. */
	public void print() {
		Node curr;
		for (curr = head; curr != null; curr = curr.next) {
			System.out.println(curr.key + " ");
		}
        System.out.println("Size is " + size);
	}
}
