//Match the user data format /api gives
interface Props{
    data?: {

    }
}

export default ({data}: Props) => {

    return (
        <div className="flex items-center h-svh">
            <div className="text-center w-full">
                <p>This is a minimal federated component inside the Fake Product integration with tailwindcss.</p>
                <p className='font-bold'>{data ? "This component received props." : "This component didn't receive any props"}</p>
            </div>
        </div>
    );
};
