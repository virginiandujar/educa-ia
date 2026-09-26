'use client';

import { useEffect, useMemo, useState } from 'react';
import {
  ArrowLeft,
  ArrowRight,
  Bot,
  Braces,
  Check,
  ChevronRight,
  CircleGauge,
  Database,
  FileCheck2,
  GitBranch,
  Hammer,
  KeyRound,
  Maximize2,
  Network,
  Play,
  Printer,
  SearchCheck,
  ShieldCheck,
  Sparkles,
  SquareTerminal,
  Users,
  Workflow,
  X,
} from 'lucide-react';

import { Button } from '@/components/ui/button';

type Slide = {
  label: string;
  eyebrow: string;
  title: string;
  kind: string;
};

const slides: Slide[] = [
  { label: 'Inicio', eyebrow: 'Tema 01 · Cultura de IA', title: 'Interacción con agentes', kind: 'cover' },
  { label: 'Concepto', eyebrow: '01 · Empecemos por lo esencial', title: 'Un agente no es un modelo con otro nombre', kind: 'formula' },
  { label: 'Interacción', eyebrow: '02 · El bucle de trabajo', title: 'Delegar no es desaparecer', kind: 'loop' },
  { label: 'Componentes', eyebrow: '03 · Qué se construye realmente', title: 'Cinco piezas, no “magia”', kind: 'components' },
  { label: 'Contrato', eyebrow: '04 · Dar contexto de calidad', title: 'Un buen encargo define los límites', kind: 'contract' },
  { label: 'Dificultad', eyebrow: '05 · Separar los niveles', title: 'Configurar un agente no es crear una plataforma', kind: 'levels' },
  { label: 'Equipo', eyebrow: '06 · La ventaja interna', title: 'El conocimiento del sistema es el activo', kind: 'knowledge' },
  { label: 'Decisión', eyebrow: '07 · Construir, integrar o contratar', title: 'Comprar aceleración, no dependencia', kind: 'decision' },
  { label: 'Preguntas', eyebrow: '08 · Evaluar una propuesta', title: 'Nueve preguntas que eliminan la ambigüedad', kind: 'questions' },
  { label: 'Piloto', eyebrow: '09 · Siguiente paso', title: 'Aprender con un piloto controlado', kind: 'pilot' },
  { label: 'Cierre', eyebrow: '10 · La idea que debe quedar', title: 'La capacidad debe permanecer en casa', kind: 'closing' },
];

const componentCards = [
  { icon: Braces, number: '01', title: 'Instrucciones', text: 'Rol, objetivo, reglas y criterios de parada.' },
  { icon: Network, number: '02', title: 'Integraciones', text: 'Repositorio, CI, incidencias y documentación.' },
  { icon: Workflow, number: '03', title: 'Flujo', text: 'Analizar, proponer, cambiar, probar y entregar.' },
  { icon: ShieldCheck, number: '04', title: 'Plataforma', text: 'Permisos, aislamiento, auditoría y costes.' },
  { icon: Users, number: '05', title: 'Conocimiento', text: 'Contexto funcional, técnico y organizativo.' },
];

const questions = [
  '¿Qué modelo usa y quién lo opera?',
  '¿Qué parte desarrolla el proveedor?',
  '¿Qué datos salen de nuestra red?',
  '¿Cómo se integra con GitLab y CI?',
  '¿Entrega instrucciones, conectores y evaluaciones?',
  '¿Recibimos el código fuente?',
  '¿Podemos modificarlo sin el proveedor?',
  '¿Qué sigue funcionando al terminar el contrato?',
  '¿Por qué no podría construirlo el equipo interno?',
];

function CoverSlide() {
  return (
    <section className="slide slide-cover">
      <div className="cover-copy">
        <p className="kicker">{slides[0].eyebrow}</p>
        <h1>{slides[0].title}</h1>
        <p className="lede">Qué son, cómo trabajar con ellos y qué capacidades conviene mantener dentro de la empresa.</p>
        <div className="key-idea">
          <span>Idea clave</span>
          <p>Un agente no es magia: es un modelo con instrucciones, contexto, herramientas y validación.</p>
        </div>
      </div>
      <AgentOrbit />
    </section>
  );
}

function AgentOrbit() {
  return (
    <div className="agent-orbit" aria-hidden="true">
      <div className="orbit orbit-one" />
      <div className="orbit orbit-two" />
      <div className="agent-core"><Sparkles /><span>AGENTE</span></div>
      <span className="orbit-tag tag-model">Modelo</span>
      <span className="orbit-tag tag-context">Contexto</span>
      <span className="orbit-tag tag-tools">Herramientas</span>
      <span className="orbit-tag tag-rules">Reglas</span>
    </div>
  );
}

function SlideHeader({ slide }: { slide: Slide }) {
  return <header className="slide-heading"><p className="kicker">{slide.eyebrow}</p><h2>{slide.title}</h2></header>;
}

function SlideContent({ slide }: { slide: Slide }) {
  if (slide.kind === 'cover') return <CoverSlide />;

  return (
    <section className={`slide content-slide slide-${slide.kind}`}>
      <SlideHeader slide={slide} />

      {slide.kind === 'formula' && (
        <div className="formula-layout">
          <div className="formula-row" aria-label="Fórmula de un agente">
            <span>Modelo</span><b>+</b><span>Instrucciones</span><b>+</b><span>Contexto</span><b>+</b><span>Herramientas</span><b>+</b><span>Validación</span>
          </div>
          <div className="myth-grid">
            <article className="myth-card no"><X /><div><strong>No es</strong><p>Un modelo nuevo entrenado para cada aplicación ni una tecnología exclusiva del proveedor.</p></div></article>
            <article className="myth-card yes"><Check /><div><strong>Sí es</strong><p>Una configuración especializada que actúa con acceso controlado y devuelve evidencia revisable.</p></div></article>
          </div>
        </div>
      )}

      {slide.kind === 'loop' && (
        <div className="loop-layout">
          <div className="loop-track">
            {[
              ['1', 'Objetivo', 'Qué resultado buscamos'],
              ['2', 'Plan', 'Cómo piensa abordarlo'],
              ['3', 'Acción', 'Usa herramientas con límites'],
              ['4', 'Verificación', 'Pruebas y controles'],
              ['5', 'Informe', 'Cambios, riesgos y dudas'],
            ].map(([number, title, text], index) => (
              <article className="loop-step" key={title}>
                <span>{number}</span><div><strong>{title}</strong><p>{text}</p></div>{index < 4 && <ChevronRight aria-hidden="true" />}
              </article>
            ))}
          </div>
          <blockquote>La persona conserva el juicio y la responsabilidad; el agente amplía la capacidad de ejecutar.</blockquote>
        </div>
      )}

      {slide.kind === 'components' && (
        <div className="component-grid">
          {componentCards.map(({ icon: Icon, number, title, text }) => (
            <article className="component-card" key={title}><div className="component-icon"><Icon /></div><span>{number}</span><h3>{title}</h3><p>{text}</p></article>
          ))}
        </div>
      )}

      {slide.kind === 'contract' && (
        <div className="contract-layout">
          <div className="code-window">
            <div className="window-bar"><i /><i /><i /><span>AGENTE.md</span></div>
            <pre><code><b>Rol:</b>{'\n'}Especialista en mantenimiento de Java heredado.{'\n\n'}<b>Objetivo:</b>{'\n'}Resolver defectos acotados y crear regresiones.{'\n\n'}<b>Reglas:</b>{'\n'}- Mantener Java 8 e interfaces públicas.{'\n'}- No añadir dependencias ni cambiar esquemas.{'\n'}- Detenerse si falta información funcional.{'\n\n'}<b>Resultado:</b>{'\n'}Cambio, pruebas, riesgos y dudas pendientes.</code></pre>
          </div>
          <div className="contract-notes">
            <p className="large-statement">La especialización empieza por un contrato de trabajo claro.</p>
            <ul><li><KeyRound />Delimita permisos</li><li><FileCheck2 />Hace verificable el resultado</li><li><SearchCheck />Define cuándo pedir ayuda</li></ul>
          </div>
        </div>
      )}

      {slide.kind === 'levels' && (
        <div className="level-stack">
          <article><span className="level-number">01</span><div><strong>Agente para un repositorio</strong><p>Días · Desarrollo · Dificultad baja/media</p></div><CircleGauge /><em>Configurar</em></article>
          <article><span className="level-number">02</span><div><strong>Integración con herramientas internas</strong><p>Semanas · Desarrollo + plataforma · Dificultad media</p></div><GitBranch /><em>Integrar</em></article>
          <article><span className="level-number">03</span><div><strong>Plataforma corporativa segura y auditada</strong><p>Meses · Plataforma + ciberseguridad · Dificultad alta</p></div><ShieldCheck /><em>Industrializar</em></article>
        </div>
      )}

      {slide.kind === 'knowledge' && (
        <div className="knowledge-layout">
          <div className="knowledge-quote"><span>“</span><p>Quien conoce la aplicación sabe qué no puede romperse.</p></div>
          <div className="knowledge-list">
            {[
              [Database, 'Decisiones históricas', 'Por qué el sistema es como es.'],
              [GitBranch, 'Interfaces críticas', 'Qué contratos deben conservarse.'],
              [SquareTerminal, 'Riesgos operativos', 'Qué cambios parecen simples y no lo son.'],
              [FileCheck2, 'Criterios de aceptación', 'Cómo demostrar que el cambio es correcto.'],
            ].map(([Icon, title, text]) => {
              const IconComponent = Icon as typeof Database;
              return <article key={String(title)}><IconComponent /><div><strong>{String(title)}</strong><p>{String(text)}</p></div></article>;
            })}
          </div>
        </div>
      )}

      {slide.kind === 'decision' && (
        <div className="decision-layout">
          <article className="decision-card internal"><span>Base interna</span><h3>Debe quedarse</h3><ul><li>Conocimiento de las aplicaciones</li><li>Instrucciones y evaluaciones</li><li>Criterios de calidad y seguridad</li><li>Capacidad de mantenimiento</li></ul></article>
          <div className="decision-bridge"><Hammer /><strong>El proveedor puede acelerar</strong><p>Implantación, integraciones, plataforma aislada o experiencia que hoy no existe.</p></div>
          <article className="decision-card external"><span>Apoyo externo</span><h3>Tiene sentido si aporta</h3><ul><li>Integración en redes restringidas</li><li>Plataforma segura y auditable</li><li>Conocimiento de tecnología antigua</li><li>Transferencia real de conocimiento</li></ul></article>
        </div>
      )}

      {slide.kind === 'questions' && (
        <ol className="question-grid">{questions.map((question, index) => <li key={question}><span>{String(index + 1).padStart(2, '0')}</span><p>{question}</p></li>)}</ol>
      )}

      {slide.kind === 'pilot' && (
        <div className="pilot-layout">
          <div className="pilot-timeline">
            <article><span>1</span><div><strong>Elegir</strong><p>Uno o dos proyectos controlados, con pruebas y responsables claros.</p></div></article>
            <article><span>2</span><div><strong>Construir</strong><p>Un agente sencillo con el equipo que mantiene la aplicación.</p></div></article>
            <article><span>3</span><div><strong>Medir</strong><p>Calidad, tiempo, seguridad, coste y esfuerzo de supervisión.</p></div></article>
            <article><span>4</span><div><strong>Decidir</strong><p>Usar la evidencia para evaluar proveedores y escalar.</p></div></article>
          </div>
          <aside className="pilot-result"><Play /><span>Resultado</span><p>Una referencia propia para saber qué comprar, qué exigir y qué conservar.</p></aside>
        </div>
      )}

      {slide.kind === 'closing' && (
        <div className="closing-layout">
          <Bot aria-hidden="true" />
          <blockquote>Desarrollar internamente la capacidad de crear y mantener agentes. Contratar, cuando esté justificado, plataforma, integración o especialización.</blockquote>
          <p>Los agentes, sus instrucciones, sus pruebas y el conocimiento de los proyectos deben permanecer bajo control de la empresa.</p>
        </div>
      )}
    </section>
  );
}

export default function Home() {
  const [current, setCurrent] = useState(0);
  const activeSlide = useMemo(() => slides[current], [current]);
  const goTo = (index: number) => setCurrent(Math.max(0, Math.min(slides.length - 1, index)));

  useEffect(() => {
    const handleKey = (event: KeyboardEvent) => {
      if (['ArrowRight', 'PageDown', ' '].includes(event.key)) { event.preventDefault(); setCurrent((value) => Math.min(value + 1, slides.length - 1)); }
      if (['ArrowLeft', 'PageUp'].includes(event.key)) { event.preventDefault(); setCurrent((value) => Math.max(value - 1, 0)); }
      if (event.key === 'Home') setCurrent(0);
      if (event.key === 'End') setCurrent(slides.length - 1);
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, []);

  return (
    <main className="presentation-shell">
      <header className="topbar">
        <button className="brand" onClick={() => goTo(0)} aria-label="Educa IA, volver al inicio"><span className="brand-mark"><Sparkles aria-hidden="true" /></span><span>Educa IA</span></button>
        <span className="topic-label">Interacción con agentes</span>
        <div className="top-actions">
          <Button className="print-button" variant="ghost" onClick={() => window.print()} aria-label="Imprimir o guardar como PDF"><Printer /><span>PDF</span></Button>
          <Button className="fullscreen-button" variant="ghost" onClick={() => document.documentElement.requestFullscreen?.()} aria-label="Ver a pantalla completa"><Maximize2 /><span>Pantalla completa</span></Button>
        </div>
      </header>

      <div className="stage" id="inicio">
        <nav className="slide-rail" aria-label="Diapositivas">
          {slides.map((item, index) => (
            <button key={item.label} className={index === current ? 'rail-item active' : 'rail-item'} onClick={() => goTo(index)} aria-current={index === current ? 'step' : undefined}>
              <span>{String(index + 1).padStart(2, '0')}</span><strong>{item.label}</strong>
            </button>
          ))}
        </nav>
        <div className="slide-viewport" aria-live="polite"><SlideContent slide={activeSlide} /></div>
      </div>

      <div className="print-deck" aria-hidden="true">
        {slides.map((slide) => <SlideContent key={slide.label} slide={slide} />)}
      </div>

      <footer className="controls">
        <span className="counter">{String(current + 1).padStart(2, '0')} / {String(slides.length).padStart(2, '0')}</span>
        <div className="progress" aria-hidden="true"><span style={{ width: `${((current + 1) / slides.length) * 100}%` }} /></div>
        <span className="keyboard-tip">Usa las flechas del teclado</span>
        <div className="control-buttons">
          <Button variant="outline" size="icon" onClick={() => goTo(current - 1)} disabled={current === 0} aria-label="Diapositiva anterior"><ArrowLeft /></Button>
          <Button size="icon" onClick={() => goTo(current + 1)} disabled={current === slides.length - 1} aria-label="Diapositiva siguiente"><ArrowRight /></Button>
        </div>
      </footer>
    </main>
  );
}
