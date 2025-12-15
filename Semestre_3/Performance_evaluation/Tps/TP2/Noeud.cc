#include "Noeud.h"
#include <cstring>

Define_Module(Noeud);

void Noeud::initialize()
{
    if (strcmp("sender", getName()) == 0) {
        cMessage *msg = new cMessage("Hello!");
        send(msg, "out");
    }
}

void Noeud::handleMessage(cMessage *msg)
{
    send(msg, "out");
}
