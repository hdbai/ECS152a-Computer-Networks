package ecs152project1;
public class Event {
	public double eventTime;
	public char eventType;
	public Event next;
	public Event prev;
	public Event(double eventTime, char eventType) {
    	this.eventTime = eventTime ;
    	this.eventType = eventType;
    }
}
