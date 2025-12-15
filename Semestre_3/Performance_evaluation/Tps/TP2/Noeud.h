#ifndef NOEUD_H_
#define NOEUD_H_

#include <omnetpp.h>

using namespace omnetpp;

class Noeud : public cSimpleModule
{
protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
};

#endif
