import UserCategories from '@/components/UserCategories'
import LogoutButton from '@/components/Logout';
import Navbar from '@/components/Navbar';
import jwt from 'jsonwebtoken';


export default function ProfilePage() {


    return (
      <div>
        <LogoutButton/>
        <header>
          <h1>miamia</h1>
        </header>
        <Navbar/>
        <UserCategories/>
        <footer></footer>
      </div>
    );
  }

  // Handles server-side rendering for the profile page
  export async function getServerSideProps(context) {

    const token = context.req.cookies.token;
    const jwtSecret = process.env.JWT_SECRET
    try {
      if (!token) {
        return {
          redirect: {
            destination: '/login',
            permanent: false,
          },
        };
      }
      jwt.verify(token, jwtSecret);
      return { props: {} };
    } catch (error) {

      return {
        redirect: {
          destination: '/login',
          permanent: false,
        },
      };
    }
  }