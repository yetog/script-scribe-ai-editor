
import { useLocation } from "react-router-dom";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      location.pathname
    );
  }, [location.pathname]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-black">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4 text-scriptRed">404</h1>
        <p className="text-xl text-white mb-4">Oops! Page not found</p>
        <Button asChild className="bg-scriptRed hover:bg-scriptRed/80">
          <a href="/">Return to Editor</a>
        </Button>
      </div>
    </div>
  );
};

export default NotFound;
