import { Sidebar } from "@/shared/components/sidebar/Sidebar"
import {Outlet} from 'react-router'

export default function MainLayout() {

    return(
        <div className="flex h-screen bg-[#f2f2f2]">
            <Sidebar />
            <main className="main-content overflow-y-auto">
                <Outlet />
            </main>
        </div>
    )
}