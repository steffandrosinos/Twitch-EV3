package Main;

import lejos.hardware.Brick;
import lejos.hardware.Button;

public class LEDColour extends Thread {
	
	public Brick myEV3;
	public boolean onGreen = false;
	public boolean onRed = false;
	public boolean onOrange = false;
	
	// LED patterns
	// 1 = Green
	// 2 = Red
	// 3 = Orange
	// 4 = Flashing Green
	// 5 = Flashing Red
	// 6 = Flashing orange
	// 7 = Heartbeat Green
	// 8 = Heartbeat Red
	// 9 = Heartbeat Orange
	
	public LEDColour(Brick myEV3) {
		this.myEV3 = myEV3;
	}
	
	public void run() {
		int time_on = -1;
		while(true) {
			if(onGreen) {
				Button.LEDPattern(4);
				time_on = 0;
				setBoolean(0, false);
			}
			if(onRed) {
				Button.LEDPattern(5);
				time_on = 0;
				setBoolean(1, false);
			}
			if(onOrange) {
				Button.LEDPattern(6);
				time_on = 0;
				setBoolean(2, false);
			}
			if(!onGreen && !onRed && !onOrange && time_on == -1) {
				Button.LEDPattern(0);
			} else {
				if(time_on >= 45000) {
					time_on = -1;
				}
			}
			try { Thread.sleep(250); } catch (Exception e) {}
			if (time_on >= 0) {
				time_on += 250;
			}
		}
    }
	
	synchronized void setBoolean(int pattern, boolean bool) {
		if(pattern == 0) {
			onGreen = bool;
		} else if(pattern == 1) {
			onRed = bool;
		} else if(pattern == 2) {
			onOrange = bool;
		}
	}
	
}