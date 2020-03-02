
public class Compass {

  public int[] position = new int[2];
  public int bearing;

  public Compass(int pos_x, int pos_y, int bearing) {
    this.position[0] = pos_y;
    this.position[1] = pos_x;
    this.bearing = bearing;
  }

  //Getters
  public int[] getPosition() {
    return this.position;
  }

  public boolean checkMove(String dir) {
    int dir_deg = getDirectionAsDeg(dir);
    int bearing_after_move = moveBearing(dir_deg);
    return checkPossible(bearing_after_move);
  }

  //function that returns degrees given direction to move, relative degree move
  public int getDirectionAsDeg(String dir) {
    if(dir.equals("Forward")) {
      return 0;
    } else if(dir.equals("Right")) {
      return 90;
    } else if(dir.equals("Left")) {
      return -90;
    } else if(dir.equals("Backwards")) {
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
    if(new_position[0] >= 0 && new_position[0] <= 6) {
      possible = true;
    }
    if(new_position[1] >= 0 && new_position[1] <= 6) {
      possible = true;
    }
    return possible;
  }

  public int[] movePosition(int[] current_pos, int dir_deg) {
    if(dir_deg == 0) {
      //Change Y+1
      current_pos[0]++;
    } else if(dir_deg == 90) {
      //Change X+1
      current_pos[1]++;
    } else if(dir_deg == 180) {
      //Change Y-1
      current_pos[0]--;
    } else if(dir_deg == 270) {
      //Change X-1
      current_pos[1]--;
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
    int dir_deg = getDirectionAsDeg(dir);
    this.bearing = moveBearing(dir_deg);
    this.position = movePosition(this.position, dir_deg);
  }

}
