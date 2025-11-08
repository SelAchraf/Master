//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

#include "Generate.h"
#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;

Define_Module(Generate);
Define_Module(Gen);
Define_Module(File);

Generate::Generate() {
    // TODO Auto-generated constructor stub

}

Generate::~Generate() {
    // TODO Auto-generated destructor stub
}


void Gen::initialize()
{
    numbrmessages=par("k");
    mean = par("lambda");
    selfMsg = new cMessage("selfMsg");  // Create a self-message
    scheduleAt(simTime() + exponential(mean), selfMsg);  // Schedule first timer

}

void Gen::handleMessage(cMessage *msg)
{
    if (msg == selfMsg) {  // Check if it's the self-message
        if (numbrmessages > 0) {
            cMessage *jobMsg = new cMessage("Hello!");
            send(jobMsg, "out");
            numbrmessages--;
            scheduleAt(simTime() + exponential(mean), selfMsg);  // Schedule next timer
        }
    }
}


void File::initialize()
{

}

void File::handleMessage(cMessage *msg)
{
    myqueue.insert(msg);
    EV << " The queue length become " << myqueue.length() <<endl;
}
