import org.omg.CORBA.ORB;
import org.omg.PortableServer.POA;
import org.omg.PortableServer.POAHelper;
import javax.naming.Context;
import javax.naming.InitialContext;
import java.util.Hashtable;

public class HelloServer {
    public static void main(String[] args) {
        ORB orb = ORB.init(args, null);
        // initialiser l'ORB

        try {
            // Configure JNDI properties for CORBA Naming Service
            Hashtable<String, String> env = new Hashtable<>();
            env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.cosnaming.CNCtxFactory");
            env.put(Context.PROVIDER_URL, "iiop://localhost:1050");
            Context ctx = new InitialContext(env);
            // il faut importer le package javax.naming

            POA rootPoa = POAHelper.narrow(orb.resolve_initial_references("RootPOA"));
            rootPoa.the_POAManager().activate();

            // instancier l'objet servant:
            HelloImpl helloImpl = new HelloImpl();

            // passer la reference orb à la méthode setORB pour que ORBShutdown puisse être appelé
            helloImpl.setORB(orb);

            ctx.rebind("RSI2020", rootPoa.servant_to_reference(helloImpl));
            /* maintenant le client utilisera RSI2020 pour retrouver la ref vers l'objet servant hello */

            System.out.println("Hello! server waiting....");
            // attendre l'invocation du client

            orb.run();
            /* l'ORB rentrera en attente après la fin de l'invocation, c'est pour cela que le client doit l'arrêter lorsqu'il termine ses appels, shutdown() */
        } catch (Exception e) {
            System.err.println("Error: " + e);
            e.printStackTrace(System.out);
        }
    }
}