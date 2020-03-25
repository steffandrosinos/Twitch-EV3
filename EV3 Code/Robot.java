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

public class Robot {

	public Server server;
	public Compass compass;
	public Game game;
	public Sirens siren;

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

		this.leftWheel = WheeledChassis.modelWheel(Motor.B, 3.5).offset(-4.5);
		this.rightWheel = WheeledChassis.modelWheel(Motor.D, 3.5).offset(4.5);
		this.myChassis = new WheeledChassis( new Wheel[]{this.leftWheel, this.rightWheel}, WheeledChassis.TYPE_DIFFERENTIAL);
		this.Pilot = new MovePilot(this.myChassis);
		this.Pilot.setLinearAcceleration(5);
		this.Pilot.setAngularAcceleration(30);
		this.Pilot.setLinearSpeed(this.FORWARD_SPEED);
		this.Pilot.setAngularSpeed(20);

		this.gyroSensor = new EV3GyroSensor(this.myEV3.getPort("S4"));
		this.spr = this.gyroSensor.getAngleMode();
		this.sample = new float[this.spr.sampleSize()];
		
		this.game = new Game();
		this.compass = new Compass(this.game, 0, 0, starting_bearing);
		this.siren = new Sirens(myEV3);
	}

	public void start() {
		this.siren.start();
		System.out.println("Started");
		while(true) {
			if(!this.moving) {
				String input = game.getInput();
				for(int i=0; i<9; i++) System.out.println("");
				if(input.equals("North") || input.equals("East") || input.equals("South") || input.equals("West")) {
					System.out.println("Dir: " + input);
					move(input);
				} else {
					if(input.equals("Spin")) {
						siren.setBoolean(true);
						this.Pilot.setAngularAcceleration(90);
						this.Pilot.setAngularSpeed(90);
						Rotate(720);
						siren.setBoolean(false);
						this.Pilot.setAngularAcceleration(30);
						this.Pilot.setAngularSpeed(20);
					} else if(input.equals("Cyan")) {
						
					} else if(input.equals("Yellow")) {
						
					} else if(input.equals("Burgandy")) {
						
					} else if(input.equals("Green")) {
						
					}
				}
			}
		}
	}

	public void move(String direction) {
		this.moving = true;
		if(compass.checkMove(direction)) {
			//Move is possible
			int turn_deg = compass.getTurnDeg(direction);
			System.out.println("Turn: " + turn_deg);
			Rotate(turn_deg);
			moveForward();
			compass.compassUpdate(direction);
			//Send coords to python
			int[] position = compass.getPosition();
			game.sendPosition(position[0], position[1]);
		} else {
			System.out.println("Not Possible");
		}
		this.moving = false;
	}

	public void moveForward() {
		this.Pilot.travel(21.2);
	}

	public void Rotate(int deg) {
		this.Pilot.rotate(deg);
	}

	public double getGyroSample() {
		this.spr.fetchSample(sample, 0);
		return (double) sample[0];
	}

}
