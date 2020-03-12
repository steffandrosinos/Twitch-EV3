package Main;

public class Compass {

	public int[][] Map = new int[6][6]; // Map[y][x]
	public int[] position = new int[2];
	public int bearing;
  
	public Compass(int pos_x, int pos_y, int bearing) {
		this.position[0] = pos_y;
		this.position[1] = pos_x;
		this.bearing = bearing;
		
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
		 // Colours
		 Map[3][1] = 2;
		 Map[5][5] = 2;
		 Map[2][0] = 3;
		 Map[4][0] = 4;
		 Map[3][4] = 5;
	}

  //Getters
	public int[] getPosition() {
		return this.position;
	}

	public boolean checkMove(String dir) {
		int bear = getDirectionAsDeg(dir);
		System.out.println("nBear: " + bear);
		return checkPossible(moveBearing(bear));
	}

	//function that returns degrees given direction to move, relative degree move
	public int getDirectionAsDeg(String dir) {
		if(dir.equals("North")) {
			return 0;
		} else if(dir.equals("East")) {
	    	return 90;
	    } else if(dir.equals("South")) {
	    	return -90;
	    } else if(dir.equals("West")) {
	    	return 180;
	    } else {
	    	return -1;
	    }
	}

  public int moveBearing(int deg) {
    int bearing_temp = this.bearing;
    int temp = bearing_temp + deg;
		if(temp >= 360) {
			bearing_temp = temp - 360;
		} else if(temp <= 0) {
			bearing_temp = temp + 360;
		} else {
			bearing_temp = temp;
		}
		if(bearing_temp == 360) {
			bearing_temp = 0;
		}
    return bearing_temp;
  }

  public boolean checkPossible(int bearing_after) {
    int[] current_pos = new int[2];
    current_pos = this.position;
    int [] new_position = movePosition(current_pos, bearing_after);
    boolean possible = false;
    System.out.println("nY: " + new_position[0] + " nX: " + new_position[1]);
    if(Map[new_position[0]][new_position[1]] != 1) {
	    if(new_position[0] >= 0 && new_position[0] <= 6) {
	      possible = true;
	    }
	    if(new_position[1] >= 0 && new_position[1] <= 6) {
	      possible = true;
	    }
    }
    return possible;
  }

  public int[] movePosition(int[] current_pos, int dir_deg) {
    if(dir_deg == 0) { 
      current_pos[0]++; //Change Y+1
    } else if(dir_deg == 90) {
      current_pos[1]++; //Change X+1
    } else if(dir_deg == 180) {
      current_pos[0]--; //Change Y-1
    } else if(dir_deg == 270) {
      current_pos[1]--; //Change X-1
    }
    return current_pos;
  }

  public void updateBearing(int deg) {
		int temp = bearing + deg;
		if(temp >= 360) {
			bearing = temp - 360;
		} else if(temp <= 0) {
			bearing = temp + 360;
		} else {
			bearing = temp;
		}

		if(bearing == 360) {
			bearing = 0;
		}
	}

	public int setDirection(String dir) {
		int bearring_after = getDirectionAsDeg(dir);
		int current_bearing = this.bearing;
		int deg = bearring_after - current_bearing;
		if(deg > 180) {
			deg = deg - 360;
		}
		return deg;
	}

  public void compassUpdate(String dir) {
    int dir_deg = getDirectionAsDeg(dir);
    this.bearing = moveBearing(dir_deg);
    this.position = movePosition(this.position, dir_deg);
    System.out.println("X: " + this.position[0] + " Y: " + this.position[1]);
  }

}
