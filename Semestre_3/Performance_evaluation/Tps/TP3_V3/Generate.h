#ifndef GENERATE_H_
#define GENERATE_H_

#include <omnetpp.h>

using namespace omnetpp;

class Generate : public cSimpleModule {
public:
    Generate();
    virtual ~Generate();
};

class Gen : public cSimpleModule{
    int numbrmessages;
    double mean;
    cMessage *selfMsg;

    protected:
        virtual void initialize();
        virtual void handleMessage(cMessage *msg);

};

class File : public cSimpleModule{
    cQueue myqueue;

    protected:
        virtual void initialize();
        virtual void handleMessage(cMessage *msg);
};

#endif
