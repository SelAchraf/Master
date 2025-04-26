import HelloApp.*;
import org.omg.CORBA.*;


class HelloImpl extends HelloPOA {
    //Créer et initialiser une instance ORB
    private ORB orb;
    public void setORB(ORB orb_val) { orb = orb_val; }

    // implement sayHello() method
    public String sayHello() { return "\nHello world !!\n"; }

    // implement shutdown() method
    public void shutdown() { orb.shutdown(false); } 
}