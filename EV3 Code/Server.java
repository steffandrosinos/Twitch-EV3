package Main;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class Server {

	//Voting
	public int move_forward = 0;
	public int move_left = 0;
	public int move_right = 0;
	public int move_backwards = 0;

	public int PORT;
	public ServerSocket server;
	public Socket client;
	public DataOutputStream dOut;
	public DataInputStream dIn;

	public Server(int PORT) {
		this.PORT = PORT;
	}

	public void connect() {
		while(true) {
			try {
				server = new ServerSocket(PORT);
				client = server.accept(); //This pauses until connection
				OutputStream out = client.getOutputStream();
				InputStream in = client.getInputStream();
				dOut = new DataOutputStream(out);
				dIn = new DataInputStream(in);
				break; //break only if a client successfully connects
			} catch(IOException e) { /* do nothing */ }
			//Delay.msDelay(100);
		}
	}

	public void close() {
		try {
			server.close();
			client.close();
			dOut.close();
			dIn.close();
		} catch(IOException e) { /* servers already closed */ }
	}

	public void reset() {
		close();
		connect();
	}

	// Function that takes a byte stream and returns "string" given 's''t''r''i''n''g''\n'
	public String getInput() {
		ArrayList<Byte> byte_list = new ArrayList<Byte>();
		while(true) {
			try {
				byte in = dIn.readByte();
				if(in != 0x0A)
					byte_list.add(in);
				else break;
			} catch (IOException e) { /* Do nothing */}
		}
		String input = "";
		for(byte byte_char : byte_list) {
			input += (char) byte_char;
    }
		return input;
	}

	public void send(String message) {
		try {
			dOut.writeBytes(message);
		} catch(IOException e) {}
	}

}
