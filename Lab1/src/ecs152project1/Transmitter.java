package ecs152project1;
import java.util.LinkedList;
import java.util.Queue;
public class Transmitter {
    private static int length; 		
	private static double time;
	private static double serverRateU = 1;
	private static double arrivalRateL = 0.2;
	public static GlobalEventList gel = null;
	public static GlobalEventList dropList = null;
	public static double serverTime;
	static Queue<Event> queue;
	public static double negExponDistrTime(double rate) {
        double temp = Math.random();
        return ((-1/rate) * Math.log(1-temp));
    }
	public static int MAXBUFFER=1;
	public static int NPDrop=0;
	public static int sum=0;
	
	public static void init(){
		length = 0;
		time = 0;	
		char type = 'a';
		gel = new GlobalEventList();
		Event first = new Event(time,type);
		gel.add(first);
		serverTime = serverTime + first.eventTime;
		queue = new LinkedList<Event>();
	}
	
	public static void processArrival(Event arrival,double currentTime){
		char type = 'a';
		double nextarrivalTime = currentTime + negExponDistrTime(arrivalRateL);			
		Event nextarrivalEvent = new Event(nextarrivalTime,type);
		gel.add(nextarrivalEvent);   
		
    	if (length == 0){
    		length++;
    		arrival.eventTime = currentTime;
    		double departEventTime = currentTime + negExponDistrTime(serverRateU);
    		Event DepartEvent = new Event(departEventTime,'d');
    		gel.add(DepartEvent); 		
    	}
    	else {
    		if(length - 1 < MAXBUFFER || MAXBUFFER == -1){
    			queue.add(arrival);
    			length++;
    		}
    		else{
    			NPDrop++;   			
    		}
    	}   		
	}
		
	public static void processDeparture(Event departure,double currentTime){	
		departure.eventTime = currentTime;
		length--;
		if(length > 0){
			Event currentPEvent; //current processing event
			currentPEvent = queue.poll();	
			currentPEvent.eventTime = time + currentPEvent.eventTime;
			double servicetime = currentTime + negExponDistrTime(serverRateU);
			serverTime = serverTime + departure.eventTime;//每次离开，服务器就busy一次，所以busytime就增加一次
			Event newDeparture = new Event(servicetime,'d');
			gel.add(newDeparture);
		}
		
	}
	
	public static void main(String[] args) {
		init();
		for (int i = 0; i < 100000; i++){
			//get the first event from the GEL;
			Event event = gel.removeFirstEvent();
			//If the event is an arrival then process-arrival-event;
			//Otherwise it must be a departure event and hence
			sum+=length*(event.eventTime-time);
			time = event.eventTime;
			if(event.eventType == 'a'){
				processArrival(event,time);
			}else{
				processDeparture(event,time);
			}
			
	//		process-service-completion;
		}
//		output-statistics;
		System.out.println(NPDrop);
		System.out.println(sum/time);
	}
}


