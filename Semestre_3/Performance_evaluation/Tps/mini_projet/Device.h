#ifndef DEVICE_H
#define DEVICE_H

#include <omnetpp.h>

using namespace omnetpp;

class Device : public cSimpleModule
{
private:
    double lambda;
    double groupSizeP;
    cMessage *generateMsg;
    int deviceId;

protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    int generateGroupSize();
};

#endif
