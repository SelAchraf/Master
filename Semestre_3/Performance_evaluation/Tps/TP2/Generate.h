#ifndef GENERATE_H_
#define GENERATE_H_

#include <omnetpp.h>

using namespace omnetpp;

class Gen : public cSimpleModule {
private:
    int numbrmessages;
    double mean;
    cMessage *selfMsg;

protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
};

class File : public cSimpleModule {
private:
    cQueue myqueue;
    simsignal_t Numberofjobs;

protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
};

#endif /* GENERATE_H_ */
