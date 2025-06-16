import ClerkProviderWithRoutes from "./auth/ClerkProviderWithRoutes.jsx"
import {Routes, Route, createBrowserRouter, RouterProvider} from "react-router-dom"
import {Layout} from "./layout/Layout.jsx"
import {ChallengeGenerator} from "./challenge/ChallengeGenerator.jsx";
import {HistoryPanel} from "./history/HistoryPanel.jsx";
import {AuthenticationPage} from "./auth/AuthenticationPage.jsx";
import './App.css'

const router = createBrowserRouter([
    {
        path: "/sign-in/*",
        element: <AuthenticationPage />
    },
    {
        path: "/sign-up",
        element: <AuthenticationPage />
    },
    {
        element: <Layout />,
        children: [
            {
                path: "/",
                element: <ChallengeGenerator />
            },
            {
                path: "/history",
                element: <HistoryPanel />
            }
        ]
    }
], {
    future: {
        v7_startTransition: true,
        v7_relativeSplatPath: true
    }
});

function App() {
    return (
        <ClerkProviderWithRoutes>
            <RouterProvider router={router} />
        </ClerkProviderWithRoutes>
    );
}

export default App
