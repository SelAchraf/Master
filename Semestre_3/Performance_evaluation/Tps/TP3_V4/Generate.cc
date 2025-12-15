#include "Generate.h"

Define_Module(Gen);
Define_Module(File);

void Gen::initialize()
{
    numbrmessages = par("jobs");
    mean = par("mean");
    selfMsg = new cMessage("selfMsg");
    scheduleAt(simTime() + exponential(mean), selfMsg);
}

void Gen::handleMessage(cMessage *msg)
{
    if (msg == selfMsg) {
        if (numbrmessages > 0) {
            cMessage *jobMsg = new cMessage("job");
            send(jobMsg, "out");
            numbrmessages--;
            if (numbrmessages > 0) {
                scheduleAt(simTime() + exponential(mean), selfMsg);
            } else {
                delete selfMsg;
                selfMsg = nullptr;
            }
        }
    }
}

void File::initialize()
{
    Numberofjobs = registerSignal("queueLength");
    EV << "*** I am ready to receive message" << endl;
}

void File::handleMessage(cMessage *msg)
{
    myqueue.insert(msg);
    EV << "The queue length became " << myqueue.getLength() << endl;
    emit(Numberofjobs, (long)myqueue.getLength());
}
