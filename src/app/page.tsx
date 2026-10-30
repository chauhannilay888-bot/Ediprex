import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import About from "@/components/About";
import Services from "@/components/Services";
import Portfolio from "@/components/Portfolio";
import YouTubeSection from "@/components/YouTubeSection";
import WhyWork from "@/components/WhyWork";
import FreeDemo from "@/components/FreeDemo";
import Workflow from "@/components/Workflow";
import Contact from "@/components/Contact";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <About />
        <Services />
        <Portfolio />
        <YouTubeSection />
        <WhyWork />
        <FreeDemo />
        <Workflow />
        <Contact />
      </main>
      <Footer />
    </>
  );
}
