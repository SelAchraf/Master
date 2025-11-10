//
// NED file for the network
//

simple File
{
    parameters:
        @signal[queueLength](type="long");
        @statistic[length](title="la longeur de la file"; source="queueLength"; record=vector,min,max,mean,sum);
        @display("i=block/queue");

    gates:
        input in;
}

simple Gen
{
    parameters:
        int k;
        double lambda;
        double T;
    gates:
        output out;
}

network Network
{
    @display("bgb=240,189");
    submodules:
        generator: Gen {
            k = 10;  // Added missing parameter
            lambda = 1.0; // Added missing parameter
            T = 1.0;
            @display("p=48,126;i=abstract/penguin");
        }
        file: File {
            @display("p=185,45");
        }
    connections:
        generator.out --> {  delay = 200ms; } --> file.in;
}
