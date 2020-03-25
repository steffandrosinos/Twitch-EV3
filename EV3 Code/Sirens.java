package Main;

import lejos.hardware.Brick;
import lejos.hardware.Button;
import lejos.hardware.Sound;

public class Sirens extends Thread {
	
	public Brick myEV3;
	public boolean siren = false;

	public Sirens(Brick myEV3) {
		this.myEV3 = myEV3;
	}
	
	public void run() {
		while(true) {
			if(!siren) {
				Button.LEDPattern(0);
				Button.LEDPattern(-1);
			}
			while(siren) {
				Button.LEDPattern(5);
				
				Sound.setVolume(15);
				
				//Sound.playTone(440, 500);
				//Sound.playTone(300, 500);
				
				Sound.playTone(440, 250);
				Sound.playTone(440, 250);
				Sound.playTone(392, 250);
				Sound.playTone(440, 250);
				try { Thread.sleep(200); } catch (Exception e) {}
				Sound.playTone(293, 250);
				try { Thread.sleep(200); } catch (Exception e) {}
				Sound.playTone(293, 250);
				Sound.playTone(440, 250);
				Sound.playTone(587, 250);
				Sound.playTone(554, 250);
				Sound.playTone(440, 250);
				
				try { Thread.sleep(500); } catch (Exception e) {}
				
			}
		}
    }
	
	synchronized void setBoolean(boolean val) {
		this.siren = val;
	}
	
}