#include "Noeud.h"
#include <cstring>  // Use <cstring> instead of <string.h>

Define_Module(Noeud);

void Noeud::initialize()
{
    if (strcmp("sender", getName()) == 0) {
        cMessage *msg = new cMessage("Hello!");
        send(msg, "out");  // This should work now with proper inheritance
    }
}

void Noeud::handleMessage(cMessage *msg)
{
    send(msg, "out");  // This should work now with proper inheritance
}
