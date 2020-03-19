package Main;

public class Compass {
	
	public int[] position = new int[2];
	public int bearing;
	public Game game;
  
	public Compass(Game game, int pos_x, int pos_y, int bearing) {
		this.game = game;
		this.position[0] = pos_y;
		this.position[1] = pos_x;
		this.bearing = bearing;
	}

  //Getters
	public int[] getPosition() {
		return this.position;
	}

	public boolean checkMove(String dir) {
		int turn = getTurnDeg(dir);
		return checkPossible(moveBearing(turn));
	}

	//function that returns degrees given direction to move, relative degree move
	public int getTurnDeg(String dir) {
		int current_bearing = this.bearing;
		int dir_bear = -1;
		if(dir.equals("North")) {
			dir_bear = 0;
		} else if(dir.equals("East")) {
			dir_bear = 90;
	    } else if(dir.equals("South")) {
	    	dir_bear = 180;
	    } else if(dir.equals("West")) {
	    	dir_bear = 270;
	    }
		int turn = dir_bear - current_bearing;
		if(turn < -180) {
			turn += 360;
		} else if(turn > 180) {
			turn -= 360;
		}
		return turn;
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
		//int[] current_pos = this.position;
		int[] current_pos = new int[2];
		current_pos[0] = this.position[0];
		current_pos[1] = this.position[1];
		int [] new_position = movePosition(current_pos, bearing_after);
		boolean possible = false;
		if(new_position[0] >= 0 && new_position[0] < 6 && new_position[1] >= 0 && new_position[1] < 6) {
			if(game.Map[new_position[0]][new_position[1]] != 1) {
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

	public void compassUpdate(String dir) {
		System.out.println("Y: " + this.position[0] + " X: " + this.position[1]);
		int dir_deg = getTurnDeg(dir);
		this.bearing = moveBearing(dir_deg);
		System.out.println("Bear: " + this.bearing);
		this.position = movePosition(this.position, this.bearing);
		System.out.println("Y: " + this.position[0] + " X: " + this.position[1]);
	}

}
