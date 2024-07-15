"use client"
import { useRouter } from 'next/navigation'

const LandingPage = () => {
    const router = useRouter()

    const handledashboardBtn = () => {
        router.push("/dashboard")
    }
     



    return (
        
        <div className="">
            <p className="">LandingPage</p>
            <button type="button" onClick={() => handledashboardBtn()}>
                dashboard
            </button>
        </div>
    );
}
export default LandingPage;