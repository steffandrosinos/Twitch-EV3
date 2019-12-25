
public class Robot {

	public int PORT;
	public Server server;
	
	public Robot(int PORT) {
		this.PORT = PORT;
		server = new Server(PORT);
	}
	
	public void start() {
		
		server.connect();
		
		String ready = server.getInput();
		while(!ready.equals("ready")) {
			ready = server.getInput();
		}
		
	}
	
}
