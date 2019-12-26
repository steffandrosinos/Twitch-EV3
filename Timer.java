
public class Timer extends Thread {

	public long start_time;
	public long current_time;
	public long timer = 0;
	
	public void start() {
		start_time = System.currentTimeMillis();
		while(true) {
			current_time = System.currentTimeMillis();
			if(current_time+35000 == start_time) {
				System.out.println("30 seonds has passed");
				start_time = System.currentTimeMillis();
				timer = 0;
			}
			timer += 1;
			try { Thread.sleep(1000); } catch(Exception e) {}
		}
	}
	
}
