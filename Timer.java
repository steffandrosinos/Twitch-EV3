
public class Timer extends Thread {

	public boolean voting = false;
	public int seconds = 0;
	
	public void run() {
		while(true) {
			while(voting) {
				seconds += 1;
				System.out.println("Timer: " + seconds);
				try { Thread.sleep(1000); } catch(Exception e) {}
			}
			seconds = 0;
			try { Thread.sleep(100); } catch(Exception e) {}
		}
	}
	
	public synchronized int getSeconds() {
		return this.seconds;
	}
	
	public synchronized boolean getVoting() {
		return this.voting;
	}
	
	public synchronized void setVoting(boolean val) {
		this.voting = val;
		return;
	}
	
}
