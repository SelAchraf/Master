simple Device
{
    parameters:
        double lambda;
        double groupSizeP;
        @display("i=device/laptop");
    gates:
        output out;
}

simple Queue
{
    parameters:
        @display("i=block/buffer");
    gates:
        input in[];      // Des devices
        output out;      // Vers serveur
        input fromServer;  // ✅ Feedback du serveur
}

simple Server
{
    parameters:
        double mu;
        @display("i=block/server");
    gates:
        input in;
        output toQueue;  // ✅ Pour notifier la queue
}

network QueueNetwork
{
    parameters:
        int numDevices = default(10);
        double lambda = default(5);
        double mu = default(8);
        double groupSizeP = default(0.3);

    submodules:
        device[numDevices]: Device {
            lambda = parent.lambda / parent.numDevices;
            groupSizeP = parent.groupSizeP;
        }
        queue: Queue;
        server: Server {
            mu = parent.mu;
        }

    connections:
        for i=0..numDevices-1 {
            device[i].out --> queue.in++;
        }
        queue.out --> server.in;
        server.toQueue --> queue.fromServer;  // ✅ Feedback loop
}