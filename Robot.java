package Main;

import lejos.hardware.Brick;
import lejos.hardware.BrickFinder;
import lejos.hardware.motor.Motor;
import lejos.hardware.sensor.EV3GyroSensor;
import lejos.robotics.SampleProvider;
import lejos.robotics.chassis.Chassis;
import lejos.robotics.chassis.Wheel;
import lejos.robotics.chassis.WheeledChassis;
import lejos.robotics.navigation.MovePilot;
import lejos.utility.Delay;

public class Robot {

	public Server server;
	
	// Variables
	public int PORT;
	public int pos_x;
	public int pos_y;
	public int bearing;
	public boolean moving = false;
	
	// Robot settings
	public Brick myEV3 = BrickFinder.getDefault();
	public Wheel leftWheel;
	public Wheel rightWheel;
	public MovePilot Pilot;
	public Chassis myChassis;
	public EV3GyroSensor gyroSensor;
	public SampleProvider spr;
	private float [] sample;
	
	public int FORWARD_SPEED = 25;
	
	public Robot(int PORT, int starting_x, int starting_y, int starting_bearing) {
		this.PORT = PORT;
		this.pos_x = starting_x;
		this.pos_y = starting_y;
		this.bearing = starting_bearing;
		
		leftWheel = WheeledChassis.modelWheel(Motor.B, 3.6).offset(-4.5);
		rightWheel = WheeledChassis.modelWheel(Motor.D, 3.6).offset(4.5);
		myChassis = new WheeledChassis( new Wheel[]{this.leftWheel, this.rightWheel}, WheeledChassis.TYPE_DIFFERENTIAL);
		Pilot = new MovePilot(this.myChassis);
		Pilot.setLinearAcceleration(10);
		Pilot.setAngularAcceleration(60);
		Pilot.setLinearSpeed(FORWARD_SPEED);
		Pilot.setAngularSpeed(90);
		
		gyroSensor = new EV3GyroSensor(myEV3.getPort("S4"));
		spr = gyroSensor.getAngleMode();
		sample = new float[spr.sampleSize()];
		
		server = new Server(PORT);
		//server.connect();
	}
	
	public void start() {
		this.Pilot.rotate(90);
		//Rotate(90);
		/*
		while(true) {
			if(!moving) {
				String direction = server.getInput();
				move(direction);
			}
		}
		*/
	}
	
	public void move(String direction) {
		moving = true;
		System.out.println("Direction: " + direction);
		if(direction.equals("Forward")) {
			System.out.println("Forward");
			moveForward();
		} else {
			System.out.println("Wasn't forward");
		}
		moving = false;
	}
	
	public void moveForward() {
		this.Pilot.travel(25);
	}
	
	// Function that rotates the robot given input degree
	public void Rotate(int deg) {
		this.Pilot.rotate(deg);
		
		//Delay.msDelay(500);
		
		double GyroReading = getGyroSample();
		double fix;
		if(deg==90||deg==-90) {
			fix = CheckRotation(GyroReading);
		}else {
			fix = CheckRotation180(GyroReading);
		}
		
		while(fix != 0) {
			this.Pilot.rotate(fix);
			//Delay.msDelay(100);
			GyroReading = getGyroSample();
			if(deg == 90 || deg == -90) {
				fix = CheckRotation(GyroReading);
			} else {
				fix = CheckRotation180(GyroReading);
			}
		}
		
		updateBearing(deg);
		gyroReset();
		
	}
	
	public void tinyRotate(int x) {
		this.Pilot.rotate(x);
		gyroReset();
	}
	
	// Rotation checking 90deg
	public static double CheckRotation(double x) {		
		double val = 0;
		if(x > 0) {
			val = 90 - x;
		} else {
			val = -90 - x;
		}
		if (val > 0.1 || val < -0.1) {
			return val;
		} else return 0;
	}
	
	public static double CheckRotation180(double x) {		
		double val = 0;
		if(x > 0) {
			val = 180 - x;
		} else {
			val = -180 - x;
		}
		if (val > 0.1 || val < -0.1) {
			return val;
		} else return 0;
	}
	
	public double getGyroSample() {
		spr.fetchSample(sample,0);
		return (double) sample[0];
	}
	
	public void gyroReset() {
		gyroSensor.reset();
	}
	
	public void updateBearing(int deg) {
		
	}
	
}
