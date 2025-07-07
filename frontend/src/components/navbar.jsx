import { useEffect, useState } from "react";
import { auth, provider, signInWithPopup, signOut } from "../firebase";

export default function Navbar() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged(setUser);
    return () => unsubscribe();
  }, []);

  return (
    <nav>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/predict">Predict</a></li>
        <li><a href="/profile">Profile</a></li>
        <li style={{ marginLeft: "auto" }}>
          {user ? (
            <>
              <span style={{ color: "white", marginRight: "10px" }}>{user.displayName}</span>
              <button onClick={() => signOut(auth)}>Logout</button>
            </>
          ) : (
            <button onClick={() => signInWithPopup(auth, provider)}>Login with Google</button>
          )}
        </li>
      </ul>
    </nav>
  );
}