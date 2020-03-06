package Main;

public class Game {

  public Server GameServer;

  public int[][] Map = new int[6][6]; // Map[y][x]

  public Game() {
    /*
     * Map Types:
     *    0 -> Empty space
     *    1 -> Block
     *    2 -> Green
     *    3 -> Blue
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
     Map[2][1] = 1;
     Map[3][0] = 1;
     Map[4][1] = 1;
     Map[3][3] = 1;
     // Colours
     Map[3][1] = 2;
     Map[5][5] = 2;
     Map[2][0] = 3;
     Map[4][0] = 4;
     Map[3][4] = 5;

     //Create Game servers
     GameServer = new Server(7767); //Check if this works as non-thread
  }

  public int getType(int[] position) {
    return Map[position[0]][position[1]];
  }

}
