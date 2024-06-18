import { useGoogleLogin } from "@react-oauth/google";

interface GoogleLoginProps {
  setToken: (token: string) => void;
}

const GoogleLogin = ({ setToken }: GoogleLoginProps) => {
  const login = useGoogleLogin({
    onSuccess: (response) => {
      console.log("oAuth response::", response);
      const token = response.access_token;
      setToken(token);
      console.log("Access Token:", token);
    },
    onError: () => console.log("Login Failed"),
  });

  return <button onClick={() => login()}>Login with Google</button>;
};

export default GoogleLogin;
