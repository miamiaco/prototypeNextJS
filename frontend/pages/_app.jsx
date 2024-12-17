import '../styles/global.css';
import { UserProvider } from '../contexts/UserContext';
import Script from 'next/script';

export default function MyApp({ Component, pageProps }) {
  return (
    <>
        {/* Google tag (gtag.js) */}
        <Script async src="https://www.googletagmanager.com/gtag/js?id=G-DLHKESPVZT"></Script>
        <Script
          id="gtag-init"
          dangerouslySetInnerHTML={{
            __html: `
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', 'G-DLHKESPVZT', {
                page_path: window.location.pathname,
              });
            `,
          }}
        />
      <UserProvider>
        <Component {...pageProps} />
      </UserProvider>
    </>
  );
}
