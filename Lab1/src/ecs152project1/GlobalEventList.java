//This is a double linked list data structure
package ecs152project1;
public class GlobalEventList {
	private Node head;
	private Node tail;
	public GlobalEventList(){
		head = new Node();
		tail = new Node();
		head.next = tail;
		tail.prev = head;
	}
	public void insert(Node node, Event item) {
        Node last = node.prev;
        Node add = new Node();
        add.value = item;
        add.next = node;
        add.prev = last;
        node.prev = add;
        last.next = add;
    }
	public void add(Event item) {
		Node tmp = new Node();
		tmp = head.next;

		if(tmp == tail)
		{
			Node add = new Node();
			add.value = item;
			add.next = tail;
			add.prev = head;
			tail.prev = add;
			head.next = add;
			return;
		}
		else if(item.eventTime < tmp.value.eventTime){
			insert(tmp,item);
		}
		else{
			while( (tmp != tail) && item.eventTime > tmp.value.eventTime)
	            {
	                tmp = tmp.next;
	            }
			insert(tmp,item);
		}	        
	}
	public Event removeFirstEvent(){
		Event temp = head.next.value;
		head.next = head.next.next;
		head.next.prev = head;	
		return temp;
	}
}

class Node{
	Event value = null;
	Node prev = null;
	Node next = null;
}