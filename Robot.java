
public class Robot {

	public int PORT;
	public Server server;
	
	public Robot(int PORT) {
		this.PORT = PORT;
		server = new Server(PORT);
	}
	
	public void start() {
		server.start();
	}
	
}
