package Main;

import lejos.hardware.Brick;

public class Game {

	public Server GameServer;

  	public int[][] Map = new int[6][6]; // Map[y][x]

	public Game() {
		/*
		 * Map Types:
		 *    0 -> Empty space
		 *    1 -> Block
		 *    2 -> Green
		 *    3 -> Yellow
		 *    4 -> Cyan
		 *    5 -> Burgundy
		 */
		// Set all of map to empty spaces
		for(int y=0; y<Map.length; y++) {
			for(int x=0; x<Map.length; x++) {
				Map[y][x] = 0;
			}
		}
		
		// Blocks
		Map[1][1] = 1;
		Map[0][2] = 1;
		Map[1][3] = 1;
		Map[3][2] = 1;
		Map[4][1] = 1;

		//Create Game servers
		GameServer = new Server(7766); //Check if this works as non-thread
		GameServer.connect();
	}

	public int getType(int[] position) {
		return Map[position[0]][position[1]];
	}
	
	public String getInput() {
		return GameServer.getInput();
	}

	public void sendPosition(int y, int x) {
		GameServer.send("" + y + "," + x);
	}

}
