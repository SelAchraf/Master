#include "Generate.h"

Define_Module(Gen);
Define_Module(File);

void Gen::initialize()
{
    numbrmessages = par("k");
    mean = par("lambda");
    selfMsg = new cMessage("selfMsg");

    // Schedule first message
    scheduleAt(simTime() + exponential(mean), selfMsg);
}

void Gen::handleMessage(cMessage *msg)
{
    if (msg == selfMsg) {
        if (numbrmessages > 0) {
            cMessage *jobMsg = new cMessage("job");
            send(jobMsg, "out");
            numbrmessages--;

            // Schedule next message if there are more
            if (numbrmessages > 0) {
                scheduleAt(simTime() + exponential(mean), selfMsg);
            } else {
                delete selfMsg; // Clean up when done
                selfMsg = nullptr;
            }
        }
    }
}

void File::initialize()
{
    Numberofjobs = registerSignal("queueLength"); // Fixed signal name
    EV << "*** I am ready to receive message" << endl;
}

void File::handleMessage(cMessage *msg)
{
    myqueue.insert(msg);
    EV << "The queue length became " << myqueue.getLength() << endl;

    emit(Numberofjobs, (long)myqueue.getLength()); // Fixed: getLength() instead of lenght

    // Note: In a real scenario, you'd also need to process/dequeue messages
}
