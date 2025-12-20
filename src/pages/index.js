import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/course/intro">
            Get Started - 5 min ⏱️
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="An advanced course on Physical AI and Humanoid Robotics">
      <HomepageHeader />
      <main>
        <section className={styles.about}>
  <div className="container padding-horiz--md">
    <div className="row">
      <div className="col col--6">
        <h2>About This Course</h2>
        <p>
          This comprehensive course explores the cutting-edge field of Physical AI and Humanoid Robotics,
          where artificial intelligence meets the physical world. Students will learn about embodied cognition,
          sensorimotor dynamics, and real-time interaction constraints that define physical intelligence systems.
        </p>
        <p>
          From foundational concepts to advanced applications, this course covers the theoretical principles
          and practical implementations necessary to understand and develop humanoid robots capable of
          intelligent interaction with their environment and humans.
        </p>
      </div>
      <div className="col col--6">
        <div className={styles.courseImage}>
          <img
            src="/img/humanoid_robot2.jpg"
            alt="Humanoid Robot"
          />
        </div>
      </div>
    </div>
  </div>
</section>
        
        <HomepageFeatures />
        
        <section className={styles.curriculum}>
          <div className="container padding-horiz--md">
            <h2 className={styles.sectionTitle}>Course Curriculum</h2>
            <div className="row">
              <div className="col col--4">
                <div className={styles.curriculumCard}>
                  <h3>Chapter 1: Foundations</h3>
                  <p>Explore the fundamental principles of Physical AI, embodied cognition, and sensorimotor dynamics.</p>
                </div>
              </div>
              <div className="col col--4">
                <div className={styles.curriculumCard}>
                  <h3>Chapter 2: Architecture</h3>
                  <p>Discover the mechanical and structural design principles of humanoid robots.</p>
                </div>
              </div>
              <div className="col col--4">
                <div className={styles.curriculumCard}>
                  <h3>Chapter 3: Control Systems</h3>
                  <p>Learn about motion planning, balance control, and dynamic stability.</p>
                </div>
              </div>
            </div>
            <div className="row" style={{marginTop: '20px'}}>
              <div className="col col--4">
                <div className={styles.curriculumCard}>
                  <h3>Chapter 4: Perception</h3>
                  <p>Understand visual, tactile, and auditory perception systems.</p>
                </div>
              </div>
              <div className="col col--4">
                <div className={styles.curriculumCard}>
                  <h3>Chapter 5: Learning</h3>
                  <p>Explore reinforcement learning, imitation learning, and adaptation.</p>
                </div>
              </div>
              <div className="col col--4">
                <div className={styles.curriculumCard}>
                  <h3>Chapter 6: Interaction</h3>
                  <p>Master human-robot interaction principles and techniques.</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}