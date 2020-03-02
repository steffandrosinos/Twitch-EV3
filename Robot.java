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
	public Compass compass;

	// Variables
	public int PORT;
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

		this.leftWheel = WheeledChassis.modelWheel(Motor.B, 3.6).offset(-4.5);
		this.rightWheel = WheeledChassis.modelWheel(Motor.D, 3.6).offset(4.5);
		this.myChassis = new WheeledChassis( new Wheel[]{this.leftWheel, this.rightWheel}, WheeledChassis.TYPE_DIFFERENTIAL);
		this.Pilot = new MovePilot(this.myChassis);
		this.Pilot.setLinearAcceleration(10);
		this.Pilot.setAngularAcceleration(60);
		this.Pilot.setLinearSpeed(this.FORWARD_SPEED);
		this.Pilot.setAngularSpeed(90);

		this.gyroSensor = new EV3GyroSensor(this.myEV3.getPort("S4"));
		this.spr = this.gyroSensor.getAngleMode();
		this.sample = new float[this.spr.sampleSize()];

		this.compass = new Compass(starting_x, starting_y, starting_bearing);
		this.server = new Server(this.PORT);
		//this.server.connect();
	}

	public void start() {
		this.Pilot.rotate(90);

		while(true) {
			if(!this.moving) {
				String direction = server.getInput();
				move(direction);
			}
		}

	}

	public void move(String direction) {
		this.moving = true;
		System.out.println("Direction: " + direction);
		if(compass.checkMove(direction)) {
			//Move is possible
			if(direction.equals("Forward")) {
				moveForward();
				compass.compassUpdate(direction);
			} else if(direction.equals("Left")) {
				moveLeft();
				compass.compassUpdate(direction);
			} else if(direction.equals("Right")) {
				moveRight();
				compass.compassUpdate(direction);
			} else if(direction.equals("Backwards")) {
				moveBackwards();
				compass.compassUpdate(direction);
			}
		} else {
			//Move not possible
		}
		this.moving = false;
	}

	public void moveForward() {
		this.Pilot.travel(25);
	}

	public void moveLeft() {
		Rotate(-90);
		this.Pilot.travel(25);
	}

	public void moveRight() {
		Rotate(90);
		this.Pilot.travel(25);
	}

	public void moveBackwards() {
		Rotate(180);
		this.Pilot.travel(25);
	}

	// Function that rotates the robot given input degree
	public void Rotate(int deg) {
		this.Pilot.rotate(deg);

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
		this.gyroSensor.reset();

	}

	public void tinyRotate(int x) {
		this.Pilot.rotate(x);
		this.gyroSensor.reset();
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
		this.spr.fetchSample(sample, 0);
		return (double) sample[0];
	}

}
