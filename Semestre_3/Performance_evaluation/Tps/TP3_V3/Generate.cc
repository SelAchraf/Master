#include "Generate.h"
#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;

Define_Module(Generate);
Define_Module(Gen);
Define_Module(File);

Generate::Generate() {
}

Generate::~Generate() {
}

void Gen::initialize()
{
    numbrmessages=par("jobs");
    mean = par("mean");
    selfMsg = new cMessage("selfMsg");
    scheduleAt(simTime() + exponential(mean), selfMsg);
}

void Gen::handleMessage(cMessage *msg)
{
    if (msg == selfMsg) {
        if (numbrmessages > 0) {
            cMessage *jobMsg = new cMessage("Hello!");
            send(jobMsg, "out");
            numbrmessages--;
            scheduleAt(simTime() + exponential(mean), selfMsg);
        }
    }
}

void File::initialize()
{
}

void File::handleMessage(cMessage *msg)
{
    myqueue.insert(msg);
    EV << " The queue length become " << myqueue.getLength() <<endl;
}
