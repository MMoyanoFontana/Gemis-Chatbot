from gradio import themes

login_css = """
:root{

  --card-bg: #16172c;
}


/* Login card mejorado */
#login-card{
  --card-w: 320px;
  margin: 5% auto;
  background: var(--card-bg);
  backdrop-filter: blur(16px);
  color:#e8edf5;
  width:max(96vw, var(--card-w));
  padding: 40px 44px 40px;
  border-radius:24px;
  border:1px solid rgba(255,255,255,.06);
  box-shadow: 
    0 32px 64px -24px rgba(2,6,23,.5),
    0 0 0 1px rgba(255,255,255,.03);
  animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both;
}

#login-title {
  font-size: 2rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 1rem;
  background: linear-gradient(90deg, #1861fc, #2b8bff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 0.02em;
}

@keyframes fadeInUp{
  from{ opacity:0; transform:translateY(30px); }
  to{ opacity:1; transform:translateY(0); }
}

#login-logo-container{
  margin: auto;
  animation: logoAppear 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  gap:0px;
}

#login-logo{
  width: 320px;
  max-width:90vw;
  margin: 0 auto;
  display: block;
}

@keyframes logoAppear{
  from{ 
    opacity:0; 
    transform:translateY(-30px) scale(0.9);
  }
  to{ 
    opacity:1; 
    transform:translateY(0) scale(1);
  }
}

/* Título y textos */
#login-card h1{ 
  margin:0 0 8px; 
  font-size: clamp(26px, 3vw, 32px); 
  line-height:1.15; 
  color:#f8fafc;
  text-align:center;
  font-weight:700;
  letter-spacing:-0.5px;
}

#login-card .subtitle{
  color:#f8fafc;
  text-align:center;
  font-size:15px;
  font-weight:600;
  margin-bottom:12px;
  transition: all .25s cubic-bezier(0.16, 1, 0.3, 1);

}

#login-card p,#login-card .gr-markdown{ 
  color:#cbd5e1; 
  font-size:14px;
  font-weight:800;
  margin-bottom:8px;
  letter-spacing:0.2px;
}

.gemis-title{
  font-size: 4rem;
  margin-block-start: 0.67em;
  margin-block-end: 0.67em;
  margin-inline-start: 0px;
  margin-inline-end: 0px;
  font-weight: bold;
  unicode-bidi: isolate;
  animation: logoAppear 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
.gemis-title span{
  background: #1861fc;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
/* Inputs mejorados */
#login-card input[type="text"],
#login-card input[type="password"],
#login-username input,
#login-password input{
  width:100%;
  padding: 14px 16px;
  border:1px solid #2a3448; 
  background:#0f1624; 
  color:#e8edf5;
  font-size:15px;
  line-height:1.4;
  outline:none;
  transition: all .25s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Botón hero mejorado */
.gr-button.gr-button--primary,
#login-btn{
  background: #1861fc !important;
  border:none !important;
  color:White !important;
  border-radius:14px;
  padding:16px 24px;
  font-weight:700;
  font-size:16px;
  letter-spacing:0.5px;
  text-transform:none;
  box-shadow: 
    0 12px 28px -8px rgba(24,97,252,0.5),
    0 0 0 1px rgba(255,255,255,0.15) inset,
    0 1px 2px 0 rgba(255,255,255,0.25) inset;
  transition: all .25s cubic-bezier(0.16, 1, 0.3, 1);
  margin-top:12px;
  cursor:pointer;
  position:relative;
  overflow:hidden;
}

.gr-button.gr-button--primary::before,
#login-btn::before{
  content:'';
  position:absolute;
  top:0;
  left:-100%;
  width:100%;
  height:100%;
  background:linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition:left 0.5s ease;
}

.gr-button.gr-button--primary:hover::before,
#login-btn:hover::before{
  left:100%;
}

.gr-button.gr-button--primary:hover,
#login-btn:hover{ 
  transform: translateY(-3px) scale(1.01); 
  box-shadow: 
    0 20px 40px -12px rgba(24,97,252,0.6),
    0 0 0 1px rgba(255,255,255,0.2) inset,
    0 1px 2px 0 rgba(255,255,255,0.3) inset;
  filter:brightness(1.1);
} 

.gr-button.gr-button--primary:active,
#login-btn:active{ 
  transform: translateY(-1px) scale(0.99); 
  box-shadow: 
    0 8px 20px -8px rgba(24,97,252,0.5),
    0 0 0 1px rgba(255,255,255,0.15) inset;
}

#login-btn[disabled]{ 
  opacity:.4; 
  cursor:not-allowed; 
  box-shadow:none;
  transform:none !important;
  filter:grayscale(1);
}


/* Mensajes mejorados */
#login-message{ 
  font-size:14px; 
  margin-top:4px; 
  padding:12px 16px;
  border-radius:12px;
  text-align:left;
  font-weight:600;
  color:#f87171;
  animation: shake .32s ease-in-out 1;

}

#login-message.error{ 
  text-color:#ff0000 !important; 
  border:1.5px solid rgba(248,113,113,0.25);
  }


/* Si el navegador soporta :has, sacude toda la card e indica error en inputs */
#login-card:has(#login-message.error){ animation: shake .32s ease-in-out 1; }

/* Shake */
@keyframes shake{
  0%{ transform:translateX(0) } 20%{ transform:translateX(-6px) }
  40%{ transform:translateX(6px) } 60%{ transform:translateX(-4px) }
  80%{ transform:translateX(4px) } 100%{ transform:translateX(0) }
}

"""

app_css = """
/* Custom CSS to adjust Gradio components */
.button-icon{
  width:20px;
  height:20px;
}

.secondary.svelte-034uhq button-icon{
  color:
  revert: invert(1)
}

.wrap.svelte-1kzox3m{
  display: flex;
  flex-direction: column;
}


#chat-list input[type="radio"] {
  display: none !important;
}


#sidebar-logo {
  padding: 10px;
}

#sidebar-logo-container {
 border-bottom: 2px solid var(--border-color-primary);
}

.label-clear-button.svelte-1rvzbk6{
  display: none !important;
  flex-shrink: 2;
}


.icon-button-wrapper.top-panel.hide-top-corner.svelte-ud4hud {
  display: none !important;
}


"""
custom_css = login_css + app_css
gemis_theme = themes.Base(
    neutral_hue="neutral",
    text_size="md",
    radius_size="xxl",
).set(
    prose_header_text_weight="500",
    prose_text_size="md",
    button_border_width="2px",
    button_primary_background_fill="#1861fc",
    button_primary_background_fill_dark="#1861fc",
    button_cancel_background_fill="#DC2626",
    button_cancel_background_fill_hover="#B91C1C",
    button_cancel_background_fill_dark="#DC2626",
    button_cancel_background_fill_hover_dark="#B91C1C",
    button_cancel_border_color="#DC2626",
    button_cancel_border_color_dark="#DC2626",
    button_cancel_text_color="White",
    button_cancel_text_color_dark="White",
    checkbox_background_color="*neutral_400",
    checkbox_background_color_selected="*neutral_200",
    checkbox_label_background_fill="none",
    checkbox_label_background_fill_hover="*neutral_200",
    checkbox_label_background_fill_dark="none",
    checkbox_background_color_dark="*neutral_200",
    checkbox_background_color_selected_dark="*primary_500",
    checkbox_label_background_fill_hover_dark="*neutral_700",
    checkbox_label_background_fill_selected="*neutral_300",
    checkbox_label_background_fill_selected_dark="*neutral_600",
    button_medium_text_weight="500",
    button_large_text_weight="500",
    button_small_text_weight="400",
    button_small_text_size="14px",
    button_medium_text_size="18px",
    checkbox_label_gap="4px",
)
