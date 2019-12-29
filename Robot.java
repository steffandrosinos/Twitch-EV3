
public class Robot {

	public int PORT;
	public Server server;
	
	public Robot(int PORT) {
		this.PORT = PORT;
		server = new Server(PORT);
		server.connect();
	}
	
	public void start() {
		while(true) {
			String direction = server.getInput();
			System.out.println("Got: " + direction);
		}
	}
	
}
